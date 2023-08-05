from typing import TYPE_CHECKING, Union

import numpy as np

if TYPE_CHECKING:  # pragma: no cover
    from docarray.typing import T
    import trimesh


class Mesh:
    FILE_EXTENSIONS = [
        'glb',
        'obj',
        'ply',
    ]
    VERTICES = 'vertices'
    FACES = 'faces'


class MeshDataMixin:
    """Provide helper functions for :class:`Document` to support 3D mesh data and point cloud."""

    def _load_mesh(
        self, force: str = None
    ) -> Union['trimesh.Trimesh', 'trimesh.Scene']:
        """Load a trimesh.Mesh or trimesh.Scene object from :attr:`.uri`.

        :param force: str or None. For 'mesh' try to coerce scenes into a single mesh. For 'scene'
            try to coerce everything into a scene.
        :return: trimesh.Mesh or trimesh.Scene object
        """
        import urllib.parse
        import trimesh

        scheme = urllib.parse.urlparse(self.uri).scheme
        loader = trimesh.load_remote if scheme in ['http', 'https'] else trimesh.load

        mesh = loader(self.uri, force=force)

        return mesh

    def load_uri_to_point_cloud_tensor(
        self: 'T', samples: int, as_chunks: bool = False
    ) -> 'T':
        """Convert a 3d mesh-like :attr:`.uri` into :attr:`.tensor`

        :param samples: number of points to sample from the mesh
        :param as_chunks: when multiple geometry stored in one mesh file,
            then store each geometry into different :attr:`.chunks`

        :return: itself after processed
        """

        if as_chunks:
            import trimesh
            from docarray.document import Document

            # try to coerce everything into a scene
            scene = self._load_mesh(force='scene')
            for geo in scene.geometry.values():
                geo: trimesh.Trimesh
                self.chunks.append(Document(tensor=np.array(geo.sample(samples))))
        else:
            # combine a scene into a single mesh
            mesh = self._load_mesh(force='mesh')
            self.tensor = np.array(mesh.sample(samples))

        return self

    def load_uri_to_vertices_and_faces(self: 'T') -> 'T':
        """Convert a 3d mesh-like :attr:`.uri` into :attr:`.chunks` as vertices and faces

        :return: itself after processed
        """
        from docarray.document import Document

        mesh = self._load_mesh(force='mesh')

        vertices = mesh.vertices.view(np.ndarray)
        faces = mesh.faces.view(np.ndarray)

        self.chunks = [
            Document(name=Mesh.VERTICES, tensor=vertices),
            Document(name=Mesh.FACES, tensor=faces),
        ]

        return self

    def load_vertices_and_faces_to_point_cloud(self: 'T', samples: int) -> 'T':
        """Convert a 3d mesh of vertices and faces from :attr:`.chunks` into point cloud :attr:`.tensor`

        :param samples: number of points to sample from the mesh
        :return: itself after processed
        """
        vertices = None
        faces = None

        for chunk in self.chunks:
            if chunk.tags['name'] == Mesh.VERTICES:
                vertices = chunk.tensor
            if chunk.tags['name'] == Mesh.FACES:
                faces = chunk.tensor

        if vertices is not None and faces is not None:
            import trimesh

            mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
            self.tensor = np.array(mesh.sample(samples))
        else:
            raise AttributeError(
                'Point cloud tensor can not be set, since vertices and faces chunk tensor have not been set.'
            )

        return self
